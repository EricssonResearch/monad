package se.uu.csproject.monadclient;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.concurrent.TimeUnit;

import se.uu.csproject.monadclient.recyclerviews.FullTripsStartTimeComparator;
import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.PartialTrip;
import se.uu.csproject.monadclient.recyclerviews.Storage;

public class StoreTrips {

    private int numberOfSearchResults, numberOfPartialTrips;
    private SimpleDateFormat format;
    private ArrayList<FullTrip> searchResults;

    // Get the trips returned by the server and store them if needed
    public ArrayList<FullTrip> storeTheTrips(JSONObject trips, boolean storeData){
        numberOfSearchResults = trips.length();
        format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        searchResults = new ArrayList<>();

        try{
            for (int i = 0; i < numberOfSearchResults; i++){
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
                    JSONArray busIDArray = partialTripJson.getJSONArray("busID");
                    ArrayList<String> trajectory = new ArrayList<>();

                    Date startTime = format.parse(partialTripJson.getString("startTime"));
                    Date endTime = format.parse(partialTripJson.getString("endTime"));
                    duration = duration + (endTime.getTime() - startTime.getTime());

                    if (trajectoryArray != null) {
                        for (int z = 0; z < trajectoryArray.length(); z++){
                            trajectory.add(trajectoryArray.getString(z));
                        }
                    }

                    int busID = busIDArray.getInt(0);

                    PartialTrip partialTrip = new PartialTrip(partialTripJson.getString("_id"),
                            partialTripJson.getInt("line"), busID,
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

                searchResults.add(fullTrip);
            }

        } catch (java.text.ParseException e){
            Log.d("oops", e.toString());

        } catch (JSONException e) {
            Log.d("oops", e.toString());
        }

        Collections.sort(searchResults, new FullTripsStartTimeComparator());
        Storage.setSearchResults(searchResults);

        // Sort the trips in ascending order based on their start time
        Collections.sort(searchResults, new FullTripsStartTimeComparator());

        if (storeData){
            Storage.setSearchResults(searchResults);
        }

        return searchResults;
    }
}
