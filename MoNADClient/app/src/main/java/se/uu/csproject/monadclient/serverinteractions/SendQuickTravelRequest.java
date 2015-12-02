package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;

import java.util.ArrayList;

import se.uu.csproject.monadclient.interfaces.AsyncResponse;
import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.Storage;


public class SendQuickTravelRequest extends AsyncTask<String, Void, ArrayList<FullTrip>>{
    public AsyncResponse delegate = null;

    /* This is the function that is called by the button listener */
    @Override
    protected ArrayList<FullTrip> doInBackground(String... params) {
        String request = "/quickRequest";
        String urlParameters = "userId=" + params[0] + "&startTime=" + params[1]
                + "&endTime=" + params[2] + "&requestTime=" + params[3]
                + "&startPositionLatitude=" + params[4] + "&startPositionLongitude=" + params[5]
                + "&edPosition=" + params[6] + "&priority=" + params[7];
        return ConnectToRequestHandler.postRequest(request, urlParameters, Storage.SEARCH_RESULTS);
    }

    /* Deal with the response returned by the server */
    @Override
    protected void onPostExecute(ArrayList<FullTrip> searchResults) {
        delegate.processFinish(searchResults);
    }
}
