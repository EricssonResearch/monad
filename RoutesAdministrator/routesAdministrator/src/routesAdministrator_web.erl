%% @author Mochi Media <dev@mochimedia.com>
%% @copyright 2010 Mochi Media <dev@mochimedia.com>

%% @doc Web server for routesAdministrator.

-module(routesAdministrator_web).
-author("Mochi Media <dev@mochimedia.com>").

-export([start/1, stop/0, loop/2, broadcast_server/0]).

%% External API

start(Options) ->
    start_broadcaster(),
    start_python(),
    start_emysql(),

    {DocRoot, Options1} = get_option(docroot, Options),
    Loop = fun (Req) ->
                   ?MODULE:loop(Req, DocRoot)
           end,
    mochiweb_http:start([{name, ?MODULE}, {loop, Loop} | Options1]).

stop() ->
    stop_python(),
    stop_emysql(),
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
    python:call(PythonInstance, mongodb_parser, start, [<<"130.238.15.114">>]),
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

start_emysql() ->
    application:start(emysql),
    emysql:add_pool(mysql_pool, [
        {size, 1},
        {user, ""},
        {password, ""},
        {host, ""},
        {port, 3306},
        {database, ""},
        {encoding, utf8}]),

    Broadcaster = whereis(broadcaster),
    Msg = [{message, "eMySQL: started"},
           {process, self()}],
    Broadcaster ! {broadcast, Msg}.

stop_emysql() ->
    application:stop(emysql),
    Broadcaster = whereis(broadcaster),
    Msg = [{message, "eMySQL: stopped"},
           {process, self()}],
    Broadcaster ! {broadcast, Msg}.

loop(Req, DocRoot) ->
    "/" ++ Path = Req:get(path),
    try
        case Req:get(method) of
            Method when Method =:= 'GET'; Method =:= 'HEAD' ->
                Req:serve_file(Path, DocRoot);
            'POST' ->
                case Path of
                    "vehicle_sign_in" ->
                        vehicle_sign_in(Req);
                    "vehicle_get_next_trip" ->
                        vehicle_get_next_trip(Req);
                    "send_notification" ->
                        Req:respond({200, [{"Content-Type", "text/plain"}], "OK"}),
                        send_notification(Req);
                    "get_passengers" ->
                        get_passengers(Req);
                    "get_traffic_information" ->
                        get_traffic_information(Req);
                    "get_traffic_information_with_params" ->
                        get_traffic_information_with_params(Req);
                    "set_google_registration_token" ->
                        set_google_registration_token(Req);
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
    Req:respond({500, [{"Content-Type", "text/plain"}], "Failed Request\n"}).

vehicle_sign_in(Req) ->
    % Parse driver_id, password, bus_line
    PostData = Req:parse_post(),
    DriverID = proplists:get_value("driver_id", PostData, "Anonymous"),
    Password = proplists:get_value("password", PostData, "Anonymous"),
    BusLine = proplists:get_value("bus_line", PostData, "Anonymous"),
    try
        % Prepare and execute client_sign_in statement
        emysql:prepare(vehicle_sign_in_statement, <<"SELECT vehicle_sign_in(?, SHA1(MD5(?)), ?)">>),
        Result = emysql:execute(mysql_pool, vehicle_sign_in_statement, [DriverID, Password, BusLine]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, vehicle_sign_in},
                       {driverID, DriverID},
                       {password, Password},
                       {busLine, BusLine},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster = whereis(broadcaster),
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
            Report = ["Failed Request: vehicle_sign_in",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

vehicle_get_next_trip(Req) ->
    PostData = Req:parse_post(),
    VehicleID_str = proplists:get_value("vehicle_id", PostData, "Anonymous"),
    {VehicleID, _} = string:to_integer(VehicleID_str),
    try
        PythonInstance = whereis(python_instance),
        Response = python:call(PythonInstance, mongodb_parser, vehicle_get_next_trip, [VehicleID]),
        % io:format("Response: ~p~n", [Response]),
        Msg = [{type, vehicle_get_next_trip},
               {vehicleID, VehicleID},
               {response, Response},
               {process, self()}],
        Broadcaster = whereis(broadcaster),
        Broadcaster ! {broadcast, Msg},
        Req:respond({200, [{"Content-Type", "text/plain"}], Response})
    catch
        Type:What ->
            Report = ["Failed Request: vehicle_get_next_trip",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
    end.

send_notification(Req) ->
    PostData = Req:parse_post(),
    VehicleID_str = proplists:get_value("vehicle_id", PostData, "Anonymous"),
    {VehicleID, _} = string:to_integer(VehicleID_str),
    % io:format("VehicleID: ~p~n", [VehicleID]),

    MessageTitle = proplists:get_value("message_title", PostData, "Anonymous"),
    % io:format("MessageTitle: ~p~n", [MessageTitle]),

    MessageBody = proplists:get_value("message_body", PostData, "Anonymous"),
    % io:format("MessageBody: ~p~n", [MessageBody]),

    try
        % Prepare and execute get_google_registration_token_statement
        emysql:prepare(get_google_registration_token_statement,
                       <<"SELECT get_google_registration_token(?)">>),
        Result = emysql:execute(mysql_pool, get_google_registration_token_statement, [VehicleID]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, send_notification},
                       {vehicleID, VehicleID},
                       {messageTitle, MessageTitle},
                       {messageBody, MessageBody},
                       {response, Response},
                       {process, self()}],
                % io:format("~n~p~n", [Msg]),
                Broadcaster = whereis(broadcaster),
                Broadcaster ! {broadcast, Msg},
                PythonInstance = whereis(python_instance),
                python:call(PythonInstance, mongodb_parser, send_notification_binary,
                            [Response, MessageTitle, MessageBody]);
            _ ->
                Msg = ["Unexpected Database Response",
                       {result, Result},
                       {trace, erlang:get_stacktrace()}],
                handle_error(Msg, Req)
        end
    catch
        Type:What ->
            Report = ["Failed Request: send_notification",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            error_logger:error_report(Report)
            % handle_error(Report, Req)
    end.

get_passengers(Req) ->
    PostData = Req:parse_post(),
    BusTripID = proplists:get_value("bus_trip_id", PostData, "Anonymous"),
    % io:format("BusTripID: ~p~n", [BusTripID]),
    CurrentBusStop = proplists:get_value("current_bus_stop", PostData, "Anonymous"),
    % io:format("CurrentBusStop: ~p~n", [CurrentBusStop]),
    NextBusStop = proplists:get_value("next_bus_stop", PostData, "Anonymous"),
    % io:format("NextBusStop: ~p~n", [NextBusStop]),
    try
        PythonInstance = whereis(python_instance),
        Response = python:call(PythonInstance, mongodb_parser, get_passengers,
                               [BusTripID, CurrentBusStop, NextBusStop]),
        Msg = [{type, get_passengers},
               {busTripID, BusTripID},
               {currentBusStop, CurrentBusStop},
               {nextBusStop, NextBusStop},
               {response, Response},
               {process, self()}],
        Broadcaster = whereis(broadcaster),
        Broadcaster ! {broadcast, Msg},
        Req:respond({200, [{"Content-Type", "text/plain"}], Response})
    catch
        Type:What ->
            Report = ["Failed Request: get_passengers",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            error_logger:error_report(Report),
            handle_error(Report, Req)
    end.

get_traffic_information(Req) ->
    try
        PythonInstance = whereis(python_instance),
        Response = python:call(PythonInstance, mongodb_parser, get_traffic_information, []),
        Msg = [{type, get_traffic_information},
               {response, Response},
               {process, self()}],
        Broadcaster = whereis(broadcaster),
        Broadcaster ! {broadcast, Msg},
        Req:respond({200, [{"Content-Type", "text/plain"}], Response})
    catch
        Type:What ->
            Report = ["Failed Request: get_traffic_information",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            error_logger:error_report(Report),
            handle_error(Report, Req)
    end.

get_traffic_information_with_params(Req) ->
    PostData = Req:parse_post(),
    SouthLatitude = proplists:get_value("south_latitude", PostData, "Anonymous"),
    % io:format("SouthLatitude: ~p~n", [SouthLatitude]),
    WestLongitude = proplists:get_value("west_longitude", PostData, "Anonymous"),
    % io:format("WestLongitude: ~p~n", [WestLongitude]),
    NorthLatitude = proplists:get_value("north_latitude", PostData, "Anonymous"),
    % io:format("NorthLatitude: ~p~n", [NorthLatitude]),
    EastLongitude = proplists:get_value("east_longitude", PostData, "Anonymous"),
    % io:format("EastLongitude: ~p~n", [EastLongitude]),
    try
        PythonInstance = whereis(python_instance),
        Response = python:call(PythonInstance, mongodb_parser, get_traffic_information_with_params,
                               [SouthLatitude, WestLongitude, NorthLatitude, EastLongitude]),
        Msg = [{type, get_traffic_information_with_params},
               {southLatitude, SouthLatitude},
               {westLongitude, WestLongitude},
               {northLatitude, NorthLatitude},
               {eastLongitude, EastLongitude},
               {response, Response},
               {process, self()}],
        Broadcaster = whereis(broadcaster),
        Broadcaster ! {broadcast, Msg},
        Req:respond({200, [{"Content-Type", "text/plain"}], Response})
    catch
        Type:What ->
            Report = ["Failed Request: get_traffic_information_with_params",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            error_logger:error_report(Report),
            handle_error(Report, Req)
    end.

set_google_registration_token(Req) ->
    PostData = Req:parse_post(),
    VehicleID_str = proplists:get_value("vehicle_id", PostData, "Anonymous"),
    {VehicleID, _} = string:to_integer(VehicleID_str),
    % io:format("VehicleID: ~p~n", [VehicleID]),
    Token = proplists:get_value("google_registration_token", PostData, "Anonymous"),
    % io:format("Token: ~p~n", [Token]),
    try
        emysql:prepare(set_google_registration_token_statement, <<"SELECT set_google_registration_token(?, ?)">>),
        Result = emysql:execute(mysql_pool, set_google_registration_token_statement, [VehicleID, Token]),
        case Result of
            {_, _, _, [[Response]], _} ->
                Msg = [{type, set_google_registration_token},
                       {vehicleID, VehicleID},
                       {token, Token},
                       {response, Response},
                       {process, self()}],
                Broadcaster = whereis(broadcaster),
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
            Report = ["Failed Request: set_google_registration_token",
                      {type, Type}, {what, What},
                      {trace, erlang:get_stacktrace()}],
            handle_error(Report, Req)
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
