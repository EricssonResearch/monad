%% @author Mochi Media <dev@mochimedia.com>
%% @copyright authentication Mochi Media <dev@mochimedia.com>

%% @doc Callbacks for the authentication application.

-module(authentication_app).
-author("Mochi Media <dev@mochimedia.com>").

-behaviour(application).
-export([start/2,stop/1]).


%% @spec start(_Type, _StartArgs) -> ServerRet
%% @doc application start callback for authentication.
start(_Type, _StartArgs) ->
    authentication_deps:ensure(),
    authentication_sup:start_link().

%% @spec stop(_State) -> ServerRet
%% @doc application stop callback for authentication.
stop(_State) ->
    ok.
