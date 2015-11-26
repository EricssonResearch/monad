%% @author Mochi Media <dev@mochimedia.com>
%% @copyright 2010 Mochi Media <dev@mochimedia.com>

%% @doc routesAdministrator.

-module(routesAdministrator).
-author("Mochi Media <dev@mochimedia.com>").
-export([start/0, stop/0]).

ensure_started(App) ->
    case application:start(App) of
        ok ->
            ok;
        {error, {already_started, App}} ->
            ok
    end.


%% @spec start() -> ok
%% @doc Start the routesAdministrator server.
start() ->
    routesAdministrator_deps:ensure(),
    ensure_started(crypto),
    application:start(routesAdministrator).


%% @spec stop() -> ok
%% @doc Stop the routesAdministrator server.
stop() ->
    application:stop(routesAdministrator).
