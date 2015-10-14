%% @author Mochi Media <dev@mochimedia.com>
%% @copyright 2010 Mochi Media <dev@mochimedia.com>

%% @doc authentication.

-module(authentication).
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
%% @doc Start the authentication server.
start() ->
    authentication_deps:ensure(),
    ensure_started(crypto),
    application:start(authentication).


%% @spec stop() -> ok
%% @doc Stop the authentication server.
stop() ->
    application:stop(authentication).
