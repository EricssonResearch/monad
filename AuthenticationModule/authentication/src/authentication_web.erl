%% @author Mochi Media <dev@mochimedia.com>
%% @copyright 2010 Mochi Media <dev@mochimedia.com>

%% @doc Web server for authentication.

-module(authentication_web).
-author("Mochi Media <dev@mochimedia.com>").

-export([start/1, stop/0, loop/3, broadcast_server/0]).

%% External API

start(Options) ->
    Broadcaster = spawn_link(?MODULE, broadcast_server, []),
    {DocRoot, Options1} = get_option(docroot, Options),
    Loop = fun (Req) ->
                   ?MODULE:loop(Req, DocRoot, Broadcaster)
           end,

    start_emysql(),
    mochiweb_http:start([{name, ?MODULE}, {loop, Loop} | Options1]).

stop() ->
    stop_emysql(),
    mochiweb_http:stop(?MODULE).

start_emysql() ->
    application:start(emysql),
    emysql:add_pool(mysql_pool, [
        {size, 1},
        {user, ""},
        {password, ""},
        {host, ""},
        {port, 3306},
        {database, ""},
        {encoding, utf8}]).

stop_emysql() ->
    application:stop(emysql).

broadcast_server() ->
    receive
        {broadcast, Message} ->
            io:format("~n~p~n", [Message]);
        Msg ->
            io:format("Unknown message: ~n~p~n", [Msg])
    end,
    erlang:hibernate(?MODULE, broadcast_server, []).

loop(Req, DocRoot, Broadcaster) ->
    "/" ++ Path = Req:get(path),
    try
        case Req:get(method) of
            Method when Method =:= 'GET'; Method =:= 'HEAD' ->
                Req:serve_file(Path, DocRoot);
            'POST' ->
                case Path of
                    "client_sign_up" ->
                        client_sign_up(Req, Broadcaster);
                    "client_sign_in" ->
                        client_sign_in(Req, Broadcaster);
                    "google_sign_in" ->
                        google_sign_in(Req, Broadcaster);
                    "client_profile_update" ->
                        client_profile_update(Req, Broadcaster);
                    "client_settings_update" ->
                        client_settings_update(Req, Broadcaster);
                    "client_existing_password_update" ->
                        client_existing_password_update(Req, Broadcaster);
                    "client_forgotten_password_reset" ->
                        client_forgotten_password_reset(Req, Broadcaster);
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

client_sign_up(Req, Broadcaster) ->
    % Parse username, password, email, phone
    PostData = Req:parse_post(),
    Username = proplists:get_value("username", PostData, "Anonymous"),
    Password = proplists:get_value("password", PostData, "Anonymous"),
    Email = proplists:get_value("email", PostData, "Anonymous"),
    Phone = proplists:get_value("phone", PostData, "Anonymous"),
    try
        % Prepare and execute client_sign_up statement
        emysql:prepare(client_sign_up_statement, <<"SELECT client_sign_up(?, SHA1(?), ?, ?)">>),
        Result = emysql:execute(mysql_pool, client_sign_up_statement, [Username, Password, Email, Phone]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_sign_up},
                       {username, Username},
                       {password, Password},
                       {email, Email},
                       {phone, Phone},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster ! {broadcast, Msg},
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

client_sign_in(Req, Broadcaster) ->
    % Parse username, password
    PostData = Req:parse_post(),
    Username = proplists:get_value("username", PostData, "Anonymous"),
    Password = proplists:get_value("password", PostData, "Anonymous"),
    try
        % Prepare and execute client_sign_in statement
        emysql:prepare(client_sign_in_statement, <<"SELECT client_sign_in(?, SHA1(?))">>),
        Result = emysql:execute(mysql_pool, client_sign_in_statement, [Username, Password]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_sign_in},
                       {username, Username},
                       {password, Password},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster ! {broadcast, Msg},
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

google_sign_in(Req, Broadcaster) ->
    % Parse email
    PostData = Req:parse_post(),
    Email = proplists:get_value("email", PostData, "Anonymous"),
    try
        % Prepare and execute google_sign_in statement
        emysql:prepare(google_sign_in_statement, <<"SELECT google_sign_in(?)">>),
        Result = emysql:execute(mysql_pool, google_sign_in_statement, [Email]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, google_sign_in},
                       {email, Email},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster ! {broadcast, Msg},
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

client_profile_update(Req, Broadcaster) ->
    % Parse client_id, username, email, phone
    PostData = Req:parse_post(),
    ClientId = proplists:get_value("client_id", PostData, "Anonymous"),
    Username = proplists:get_value("username", PostData, "Anonymous"),
    Email = proplists:get_value("email", PostData, "Anonymous"),
    Phone = proplists:get_value("phone", PostData, "Anonymous"),
    try
        % Prepare and execute client_sign_up statement
        emysql:prepare(client_profile_update_statement, <<"SELECT client_profile_update(?, ?, ?, ?)">>),
        Result = emysql:execute(mysql_pool, client_profile_update_statement,
                                [ClientId, Username, Email, Phone]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_profile_update},
                       {username, Username},
                       {email, Email},
                       {phone, Phone},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster ! {broadcast, Msg},
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

client_settings_update(Req, Broadcaster) ->
    % Parse client_id, language, store_location, notifications_alert, recommendations_alert, theme
    PostData = Req:parse_post(),
    ClientId = proplists:get_value("client_id", PostData, "Anonymous"),
    Language = proplists:get_value("language", PostData, "Anonymous"),
    StoreLocation = proplists:get_value("store_location", PostData, "Anonymous"),
    NotificationsAlert = proplists:get_value("notifications_alert", PostData, "Anonymous"),
    RecommendationsAlert = proplists:get_value("recommendations_alert", PostData, "Anonymous"),
    Theme = proplists:get_value("theme", PostData, "Anonymous"),
    try
        % Prepare and execute client_sign_up statement
        emysql:prepare(client_settings_update_statement, <<"SELECT client_settings_update(?, ?, ?, ?, ?, ?)">>),
        Result = emysql:execute(mysql_pool, client_settings_update_statement,
                                [ClientId, Language, StoreLocation, NotificationsAlert, RecommendationsAlert, Theme]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_settings_update},
                       {clientId, ClientId},
                       {language, Language},
                       {storeLocation, StoreLocation},
                       {notificationsAlert, NotificationsAlert},
                       {recommendationsAlert, RecommendationsAlert},
                       {theme, Theme},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster ! {broadcast, Msg},
                Req:respond({200, [{"Content-Type", "text/plain"}], Response});
            _ ->
                Msg = ["Unexpected Database Response",
                       {result, Result},
                       {trace, erlang:get_stacktrace()}],
                handle_error(Msg, Req)
        end
    catch
        Type:What ->
            Report = ["Failed Request: client_settings_update",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

client_existing_password_update(Req, Broadcaster) ->
    % Parse client_id, old_password, new_password
    PostData = Req:parse_post(),
    ClientId = proplists:get_value("client_id", PostData, "Anonymous"),
    OldPassword = proplists:get_value("old_password", PostData, "Anonymous"),
    NewPassword = proplists:get_value("new_password", PostData, "Anonymous"),
    try
        % Prepare and execute client_existing_password_update statement
        emysql:prepare(client_existing_password_update_statement,
                       <<"SELECT client_existing_password_update(?, ?, ?)">>),
        Result = emysql:execute(mysql_pool, client_existing_password_update_statement,
                                [ClientId, OldPassword, NewPassword]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_existing_password_update},
                       {clientId, ClientId},
                       {oldPassword, OldPassword},
                       {newPassword, NewPassword},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster ! {broadcast, Msg},
                Req:respond({200, [{"Content-Type", "text/plain"}], Response});
            _ ->
                Msg = ["Unexpected Database Response",
                       {result, Result},
                       {trace, erlang:get_stacktrace()}],
                handle_error(Msg, Req)
        end
    catch
        Type:What ->
            Report = ["Failed Request: client_existing_password_update",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

client_forgotten_password_reset(Req, Broadcaster) ->
    % Parse email, new_password
    PostData = Req:parse_post(),
    Email = proplists:get_value("email", PostData, "Anonymous"),
    NewPassword = proplists:get_value("new_password", PostData, "Anonymous"),
    try
        % Prepare and execute client_existing_password_update statement
        emysql:prepare(client_forgotten_password_reset_statement,
                       <<"SELECT client_forgotten_password_reset(?, ?)">>),
        Result = emysql:execute(mysql_pool, client_forgotten_password_reset_statement,
                                [Email, NewPassword]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, client_forgotten_password_reset},
                       {email, Email},
                       {newPassword, NewPassword},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster ! {broadcast, Msg},
                Req:respond({200, [{"Content-Type", "text/plain"}], Response});
            _ ->
                Msg = ["Unexpected Database Response",
                       {result, Result},
                       {trace, erlang:get_stacktrace()}],
                handle_error(Msg, Req)
        end
    catch
        Type:What ->
            Report = ["Failed Request: client_forgotten_password_reset",
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
