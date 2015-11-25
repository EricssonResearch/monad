%% @author Mochi Media <dev@mochimedia.com>
%% @copyright routesAdministrator Mochi Media <dev@mochimedia.com>

%% @doc Callbacks for the routesAdministrator application.

-module(routesAdministrator_app).
-author("Mochi Media <dev@mochimedia.com>").

-behaviour(application).
-export([start/2,stop/1]).


%% @spec start(_Type, _StartArgs) -> ServerRet
%% @doc application start callback for routesAdministrator.
start(_Type, _StartArgs) ->
    routesAdministrator_deps:ensure(),
    routesAdministrator_sup:start_link().

%% @spec stop(_State) -> ServerRet
%% @doc application stop callback for routesAdministrator.
stop(_State) ->
    ok.
