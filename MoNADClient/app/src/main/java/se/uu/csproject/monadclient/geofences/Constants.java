/**
 * Copyright 2014 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * This code was taken from: https://github.com/googlesamples/android-play-location/tree/master/Geofencing
 * It was modified according to the needs of the project.
 */

package se.uu.csproject.monadclient.geofences;

import com.google.android.gms.maps.model.LatLng;

import java.util.ArrayList;
import java.util.HashMap;

import se.uu.csproject.monadclient.storage.BusStop;
import se.uu.csproject.monadclient.storage.Storage;

public class Constants {
    public static final String PACKAGE_NAME = "com.google.android.gms.location.Geofence";
    public static final String SHARED_PREFERENCES_NAME = PACKAGE_NAME + ".SHARED_PREFERENCES_NAME";
    public static final String GEOFENCES_ADDED_KEY = PACKAGE_NAME + ".GEOFENCES_ADDED_KEY";
    public static final long GEOFENCE_EXPIRATION_IN_HOURS = 12;
    public static final long GEOFENCE_EXPIRATION_IN_MILLISECONDS = GEOFENCE_EXPIRATION_IN_HOURS * 60 * 60 * 1000;
    public static final float GEOFENCE_RADIUS_IN_METERS = 50;
    public static final HashMap<String, LatLng> UPPSALA_LANDMARKS = new HashMap<String, LatLng>();

    public static void initializeGeofences(){
        ArrayList<BusStop> busStops = Storage.getBusStops();
        for (int i = 0; i < busStops.size(); i++){
            UPPSALA_LANDMARKS.put(busStops.get(i).getName(), new LatLng(busStops.get(i).getLatitude(),
                                   busStops.get(i).getLongitude()));
        }
    }
}
