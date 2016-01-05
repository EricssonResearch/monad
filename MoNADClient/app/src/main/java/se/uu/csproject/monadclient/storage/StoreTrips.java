package se.uu.csproject.monadclient.storage;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.concurrent.TimeUnit;

import se.uu.csproject.monadclient.FullTripsStartTimeComparator;

public class StoreTrips {

    private int numberOfResults, numberOfPartialTrips;
    private String TAG = "oops";
    private SimpleDateFormat format;
    private ArrayList<FullTrip> results;

    // Get the trips returned by the server and store them
    public ArrayList<FullTrip> storeTheTrips(JSONObject trips, int searchResultsOrBookings){
        numberOfResults = trips.length();
        format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        results = new ArrayList<>();

        try{
            for (int i = 0; i < numberOfResults; i++){
                String tripID = "", requestID = "";
                long duration = 0;
                int feedback = -1;
                boolean booked = false;

                JSONArray fullTripJson = trips.getJSONArray(Integer.toString(i+1));
                ArrayList<PartialTrip> partialTripArrayList = new ArrayList<>();
                numberOfPartialTrips = fullTripJson.length();

                // Store the partial trips into a full trip
                for (int y = 0; y < numberOfPartialTrips; y++){
                    JSONObject partialTripJson = fullTripJson.getJSONObject(y);
                    JSONArray trajectoryArray = partialTripJson.getJSONArray("trajectory");
                    ArrayList<String> trajectory = new ArrayList<>();

                    Date startTime = format.parse(partialTripJson.getString("startTime"));
                    Date endTime = format.parse(partialTripJson.getString("endTime"));
                    duration = duration + (endTime.getTime() - startTime.getTime());

                    if (trajectoryArray != null) {
                        for (int z = 0; z < trajectoryArray.length(); z++){
                            trajectory.add(trajectoryArray.getString(z));
                        }
                    }

                    PartialTrip partialTrip = new PartialTrip(partialTripJson.getString("_id"),
                            partialTripJson.getInt("line"), partialTripJson.getInt("busID"),
                            partialTripJson.getString("startBusStop"), startTime,
                            partialTripJson.getString("endBusStop"), endTime, trajectory);

                    if (y == 0){
                        feedback = partialTripJson.getInt("feedback");
                        tripID = partialTripJson.getString("_id");
                        requestID = partialTripJson.getString("requestID");
                        booked = partialTripJson.getBoolean("booked");
                    }
                    partialTripArrayList.add(partialTrip);
                }

                long durationInMinutes = TimeUnit.MILLISECONDS.toMinutes(duration);

                FullTrip fullTrip = new FullTrip(tripID, requestID, partialTripArrayList,
                        durationInMinutes, booked, feedback);

                results.add(fullTrip);
            }

        } catch (java.text.ParseException e){
            Log.d(TAG, e.toString());

        } catch (JSONException e) {
            Log.d(TAG, e.toString());
        }

        // Sort the trips based on their start time and whether they're new or old
        Collections.sort(results, new FullTripsStartTimeComparator());

        if (searchResultsOrBookings == Storage.SEARCH_RESULTS){
            Storage.setSearchResults(results);
        } else if (searchResultsOrBookings == Storage.BOOKINGS){
            Storage.setBookings(results);
        }

        return results;
    }
}
