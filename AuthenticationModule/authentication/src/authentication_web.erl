%% @author Mochi Media <dev@mochimedia.com>
%% @copyright 2010 Mochi Media <dev@mochimedia.com>

%% @doc Web server for authentication.

-module(authentication_web).
-author("Mochi Media <dev@mochimedia.com>").

-export([start/1, stop/0, loop/2]).

%% External API

start(Options) ->
    {DocRoot, Options1} = get_option(docroot, Options),
    Loop = fun (Req) ->
                   ?MODULE:loop(Req, DocRoot)
           end,

    crypto:start(),
    application:start(emysql),
    emysql:add_pool(pool_one, [
        {size, 1},
        {user, ""},
        {password, ""},
        {host, ""},
        {port, 3306},
        {database, ""},
        {encoding, utf8}]),

    mochiweb_http:start([{name, ?MODULE}, {loop, Loop} | Options1]).

stop() ->
    mochiweb_http:stop(?MODULE).

loop(Req, DocRoot) ->
    "/" ++ Path = Req:get(path),
    try
        case Req:get(method) of
            Method when Method =:= 'GET'; Method =:= 'HEAD' ->
                case Path of
                  "hello_world" ->
                    Req:respond({200, [{"Content-Type", "text/plain"}], "Hello world!\n"});
                    _ ->
                        Req:serve_file(Path, DocRoot)
                end;
            'POST' ->
                case Path of
                    "client_sign_up" ->
                        client_sign_up(Req);
                    "client_sign_in" ->
                        client_sign_in(Req);
                    "google_sign_in" ->
                        google_sign_in(Req);
                    _ ->
                        Req:not_found()
                end;
            _ ->
                Req:respond({501, [], []})
        end
    catch
        Type:What ->
            Report = ["Failed Request: loop",
                      {path, Path},
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

client_sign_up(Req) ->
    % Parse username, password, email, phone
    PostData = Req:parse_post(),
    Username = proplists:get_value("username", PostData, "Anonymous"),
    Password = proplists:get_value("password", PostData, "Anonymous"),
    Email = proplists:get_value("email", PostData, "Anonymous"),
    Phone = proplists:get_value("phone", PostData, "Anonymous"),
    try
        % Prepare and execute client_sign_up statement
        emysql:prepare(client_sign_up_statement, <<"SELECT client_sign_up(?, SHA1(?), ?, ?)">>),
        Result = emysql:execute(pool_one, client_sign_up_statement, [Username, Password, Email, Phone]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_sign_up},
                       {username, Username},
                       {password, Password},
                       {email, Email},
                       {phone, Phone},
                       {response, Response},
                       {process, self()}],
                io:format("~n~p~n", [Msg]),
                Req:respond({200, [{"Content-Type", "text/plain"}], Response});
            _ ->
                Msg = ["Unexpected Database Response",
                       {result, Result},
                       {trace, erlang:get_stacktrace()}],
                handle_error(Msg, Req)
        end
    catch
        Type:What ->
            Report = ["Failed Request: client_sign_up",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

client_sign_in(Req) ->
    % Parse username, password
    PostData = Req:parse_post(),
    Username = proplists:get_value("username", PostData, "Anonymous"),
    Password = proplists:get_value("password", PostData, "Anonymous"),
    try
        % Prepare and execute client_sign_in statement
        emysql:prepare(client_sign_in_statement, <<"SELECT client_sign_in(?, SHA1(?))">>),
        Result = emysql:execute(pool_one, client_sign_in_statement, [Username, Password]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_sign_in},
                       {username, Username},
                       {password, Password},
                       {response, Response},
                       {process, self()}],
                io:format("~n~p~n", [Msg]),
                Req:respond({200, [{"Content-Type", "text/plain"}], Response});
            _ ->
                Msg = ["Unexpected Database Response",
                       {result, Result},
                       {trace, erlang:get_stacktrace()}],
                handle_error(Msg, Req)
        end
    catch
        Type:What ->
            Report = ["Failed Request: client_sign_in",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

google_sign_in(Req) ->
    % Parse email
    PostData = Req:parse_post(),
    Email = proplists:get_value("email", PostData, "Anonymous"),
    try
        % Prepare and execute google_sign_in statement
        emysql:prepare(client_sign_up_statement, <<"SELECT google_sign_in(?)">>),
        Result = emysql:execute(pool_one, client_sign_up_statement, [Email]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, google_sign_in},
                       {email, Email},
                       {response, Response},
                       {process, self()}],
                io:format("~n~p~n", [Msg]),
                Req:respond({200, [{"Content-Type", "text/plain"}], Response});
            _ ->
                Msg = ["Unexpected Database Response",
                       {result, Result},
                       {trace, erlang:get_stacktrace()}],
                handle_error(Msg, Req)
        end
    catch
        Type:What ->
            Report = ["Failed Request: google_sign_in",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

client_profile_update(Req) ->
    % Parse username, password, email, phone
    PostData = Req:parse_post(),
    ClientId = proplists:get_value("client_id", PostData, "Anonymous"),
    Username = proplists:get_value("username", PostData, "Anonymous"),
    Email = proplists:get_value("email", PostData, "Anonymous"),
    Phone = proplists:get_value("phone", PostData, "Anonymous"),
    try
        % Prepare and execute client_sign_up statement
        emysql:prepare(client_profile_update_statement, <<"SELECT client_profile_update(?, ?, ?, ?)">>),
        Result = emysql:execute(pool_one, client_profile_update_statement,
                                [ClientId, Username, Email, Phone]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_profile_update},
                       {username, Username},
                       {email, Email},
                       {phone, Phone},
                       {response, Response},
                       {process, self()}],
                io:format("~n~p~n", [Msg]),
                Req:respond({200, [{"Content-Type", "text/plain"}], Response});
            _ ->
                Msg = ["Unexpected Database Response",
                       {result, Result},
                       {trace, erlang:get_stacktrace()}],
                handle_error(Msg, Req)
        end
    catch
        Type:What ->
            Report = ["Failed Request: client_profile_update",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

handle_error(Report, Req) ->
    error_logger:error_report(Report),
    Req:respond({500, [{"Content-Type", "text/plain"}], "Failed Request\n"}).

%% Internal API

get_option(Option, Options) ->
    {proplists:get_value(Option, Options), proplists:delete(Option, Options)}.

%%
%% Tests
%%
-ifdef(TEST).
-include_lib("eunit/include/eunit.hrl").

you_should_write_a_test() ->
    ?assertEqual(
       "No, but I will!",
       "Have you written any tests?"),
    ok.

-endif.
