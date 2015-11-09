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

import se.uu.csproject.monadclient.recyclerviews.CustomComparator;
import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.PartialTrip;
import se.uu.csproject.monadclient.recyclerviews.Storage;

public class StoreTrips {

    private int numberOfSearchResults, numberOfPartialTrips;
    private SimpleDateFormat format;
    private ArrayList<FullTrip> searchResults;

    public ArrayList<FullTrip> storeTheTrips(JSONObject trips){
        // Store the recommended (full) trips from the server
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
                    ArrayList<String> trajectory = new ArrayList<>();

                    Date startTime = format.parse(partialTripJson.getString("startTime"));
                    Date endTime = format.parse(partialTripJson.getString("endTime"));
                    duration = duration + (endTime.getTime() - startTime.getTime());

                    if (trajectoryArray != null) {
                        for (int z = 0; z < trajectoryArray.length(); z++){
                            trajectory.add(trajectoryArray.getString(z));
                        }
                    }

                    PartialTrip partialTrip = new PartialTrip(partialTripJson.getInt("line"),
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

        Collections.sort(searchResults, new CustomComparator());
        Storage.setSearchResults(searchResults);
        return searchResults;
    }
}
