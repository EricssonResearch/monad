package se.uu.csproject.monadclient.geofences;

import com.google.android.gms.maps.model.LatLng;

import java.util.HashMap;

public class Constants {
    private Constants() {
    }

    public static final String PACKAGE_NAME = "com.google.android.gms.location.Geofence";

    public static final String SHARED_PREFERENCES_NAME = PACKAGE_NAME + ".SHARED_PREFERENCES_NAME";

    public static final String GEOFENCES_ADDED_KEY = PACKAGE_NAME + ".GEOFENCES_ADDED_KEY";

    /**
     * Used to set an expiration time for a geofence. After this amount of time Location Services
     * stops tracking the geofence.
     */
    public static final long GEOFENCE_EXPIRATION_IN_HOURS = 12;

    /**
     * For this sample, geofences expire after twelve hours.
     */
    public static final long GEOFENCE_EXPIRATION_IN_MILLISECONDS =
            GEOFENCE_EXPIRATION_IN_HOURS * 60 * 60 * 1000;
    public static final float GEOFENCE_RADIUS_IN_METERS = 50;

    /**
     * Map for storing information about airports in the San Francisco bay area.
     */
    public static final HashMap<String, LatLng> UPPSALA_LANDMARKS = new HashMap<String, LatLng>();
    static {
        // Polacksbacken Hus 4
        UPPSALA_LANDMARKS.put("HUS4", new LatLng(59.841016, 17.648589));

        // Rullan
        UPPSALA_LANDMARKS.put("RULLAN", new LatLng(59.840851, 17.650110));


    }
}
