package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.interfaces.AsyncGetBusStopsInteraction;

public class GetBusStopsTask extends AsyncTask <Void, Void, String> {
    AsyncGetBusStopsInteraction callingClass;

    public GetBusStopsTask(AsyncGetBusStopsInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        return ClientAuthentication.postGetBusStopsRequest();
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
