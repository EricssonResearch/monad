%% @author Mochi Media <dev@mochimedia.com>
%% @copyright routesGenerator Mochi Media <dev@mochimedia.com>

%% @doc Callbacks for the routesGenerator application.

-module(routesGenerator_app).
-author("Mochi Media <dev@mochimedia.com>").

-behaviour(application).
-export([start/2,stop/1]).


%% @spec start(_Type, _StartArgs) -> ServerRet
%% @doc application start callback for routesGenerator.
start(_Type, _StartArgs) ->
    routesGenerator_deps:ensure(),
    routesGenerator_sup:start_link().

%% @spec stop(_State) -> ServerRet
%% @doc application stop callback for routesGenerator.
stop(_State) ->
    ok.
