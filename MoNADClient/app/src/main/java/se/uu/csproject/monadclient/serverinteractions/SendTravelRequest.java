package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;
import java.util.ArrayList;

import se.uu.csproject.monadclient.interfaces.AsyncResponse;
import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.Storage;


public class SendTravelRequest extends AsyncTask<String, Void, ArrayList<FullTrip>> {
    public AsyncResponse delegate = null;

    /* This is the function that is called by the button listener */
    @Override
    protected ArrayList<FullTrip> doInBackground(String... params) {
        String request = "/request";
        String urlParameters = "userId=" + params[0] + "&startTime=" + params[1] + "&endTime=" + params[2]
                + "&requestTime=" + params[3] + "&stPosition=" + params[4] + "&edPosition=" + params[5]
                + "&priority=" + params[6] + "&startPositionLatitude=" + params[7]
                + "&startPositionLongitude=" + params[8];
        return ConnectToRequestHandler.postRequest(request, urlParameters, Storage.SEARCH_RESULTS);
    }

    /* Deal with the response returned by the server */
    @Override
    protected void onPostExecute(ArrayList<FullTrip> searchResults) {
        delegate.processFinish(searchResults);
    }
}


