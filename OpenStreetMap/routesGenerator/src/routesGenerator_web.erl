%% @author Mochi Media <dev@mochimedia.com>
%% @copyright 2010 Mochi Media <dev@mochimedia.com>

%% @doc Web server for routesGenerator.

-module(routesGenerator_web).
-author("Mochi Media <dev@mochimedia.com>").

-export([start/1, stop/0, loop/2, broadcast_server/0]).

%% External API

start(Options) ->
    start_broadcaster(),
    start_python(),

    {DocRoot, Options1} = get_option(docroot, Options),
    Loop = fun (Req) ->
                   ?MODULE:loop(Req, DocRoot)
           end,
    mochiweb_http:start([{name, ?MODULE}, {loop, Loop} | Options1]).

stop() ->
    stop_python(),
    stop_broadcaster(),
    mochiweb_http:stop(?MODULE).

start_broadcaster() ->
    Broadcaster = spawn_link(?MODULE, broadcast_server, []),
    register(broadcaster, Broadcaster),
    Msg = [{message, "Broadcaster: started"},
           {process, Broadcaster}],
    Broadcaster ! {broadcast, Msg}.

broadcast_server() ->
    receive
        {broadcast, Message} ->
            io:format("~n~p~n", [Message]);
        Msg ->
            io:format("~nBroadcaster - Unknown message: ~p~n", [Msg])
    end,
    erlang:hibernate(?MODULE, broadcast_server, []).

stop_broadcaster() ->
    Broadcaster = whereis(broadcaster),
    exit(Broadcaster, normal),
    Msg = [{message, "Broadcaster: stopped"},
           {process, Broadcaster}],
    io:format("~n~p~n", [Msg]).

start_python() ->
    {ok, PythonInstance} = python:start([{python_path, "src/python"}]),
    register(python_instance, PythonInstance),
    python:call(PythonInstance, rooter, start, []),
    Broadcaster = whereis(broadcaster),
    Msg = [{message, "PythonInstance: started"},
           {process, PythonInstance}],
    Broadcaster ! {broadcast, Msg}.

stop_python() ->
    PythonInstance = whereis(python_instance),
    python:stop(PythonInstance),
    Broadcaster = whereis(broadcaster),
    Msg = [{message, "PythonInstance: stopped"},
           {process, PythonInstance}],
    Broadcaster ! {broadcast, Msg}.

loop(Req, DocRoot) ->
    "/" ++ Path = Req:get(path),
    try
        case Req:get(method) of
            Method when Method =:= 'GET'; Method =:= 'HEAD' ->
                Req:serve_file(Path, DocRoot);
            'POST' ->
                case Path of
                    "get_nearest_stop" ->
                        get_nearest_stop(Req);
                    "get_nearest_stop_from_coordinates" ->
                        get_nearest_stop_from_coordinates(Req);
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

handle_error(Report, Req) ->
    error_logger:error_report(Report),
    Req:respond({500, [{"Content-Type", "text/plain"}], "Failed 1Request\n"}).

get_nearest_stop(Req) ->
    PostData = Req:parse_post(),
    Address = proplists:get_value("address", PostData, "Anonymous"),
    PythonInstance = whereis(python_instance),
    PythonInstance ! {<<"get_nearest_stop">>, Address, self()},
    receive
        {ok, Response} ->
            io:format("~nResponse: ~p~n", [Response]),
            Req:respond({200, [{"Content-Type", "text/plain"}], Response});
        Other ->
            Msg = ["Unexpected get_nearest_stop response",
                   {response, Other},
                   {trace, erlang:get_stacktrace()}],
            handle_error(Msg, Req)
    end.

get_nearest_stop_from_coordinates(Req) ->
    PostData = Req:parse_post(),
    Longitude = proplists:get_value("lon", PostData, "Anonymous"),
    Latitude = proplists:get_value("lat", PostData, "Anonymous"),
    PythonInstance = whereis(python_instance),
    PythonInstance ! {<<"get_nearest_stop_from_coordinates">>, Longitude, Latitude, self()},
    receive
        {ok, Response} ->
            Req:respond({200, [{"Content-Type", "text/plain"}], Response});
        Other ->
            Msg = ["Unexpected get_nearest_stop_from_coordinates response",
                    {response, Other},
                    {trace, erlang:get_stacktrace()}],
            handle_error(Msg, Req)
    end.

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
