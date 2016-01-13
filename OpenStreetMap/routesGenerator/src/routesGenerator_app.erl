%% Copyright 2015 Ericsson AB
%%
%% Licensed under the Apache License, Version 2.0 (the "License"); you may not
%% use this file except in compliance with the License. You may obtain a copy
%% of the License at
%%
%%    http://www.apache.org/licenses/LICENSE-2.0
%%
%% Unless required by applicable law or agreed to in writing, software
%% distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
%% WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
%% License for the specific language governing permissions and limitations
%% under the License.

%% @doc The following file is based on MochiWeb (Available at: https://github.com/mochi/mochiweb)
%%      @author Mochi Media <dev@mochimedia.com>
%%      @copyright 2010 Mochi Media <dev@mochimedia.com>

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
