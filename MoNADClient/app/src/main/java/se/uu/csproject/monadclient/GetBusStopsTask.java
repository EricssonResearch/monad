package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

/**
 *
 */
public class GetBusStopsTask extends AsyncTask <Void, Void, String> {
    AsyncGetBusStopsInteraction callingClass;

    public GetBusStopsTask(AsyncGetBusStopsInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        return "0";
    }

    @Override
    protected void onPostExecute(String response) {
        if (response.equals("1")) {
            Log.d(callingClass.getClass().getCanonicalName(),
                    "BusStops have been successfully loaded by the database");
            callingClass.processReceivedGetBusStopsResponse();
        }
        else {
            Log.d(callingClass.getClass().getCanonicalName(),
                    "BusStops have not been loaded");
        }
    }
}
