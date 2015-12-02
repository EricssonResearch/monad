package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;

import java.util.ArrayList;

import se.uu.csproject.monadclient.interfaces.AsyncResponse;
import se.uu.csproject.monadclient.storage.FullTrip;
import se.uu.csproject.monadclient.storage.Storage;

public class SendUserBookingsRequest extends AsyncTask<String, Void, ArrayList<FullTrip>> {
    public AsyncResponse delegate = null;

    /* This is the function that is called by the button listener */
    @Override
    protected ArrayList<FullTrip> doInBackground(String... params) {
        String request = "/getUserBookingsRequest";
        String urlParameters = "userId=" + params[0];
        return ConnectToRequestHandler.postRequest(request, urlParameters, Storage.BOOKINGS);
    }

    /* Deal with the response returned by the server */
    @Override
    protected void onPostExecute(ArrayList<FullTrip> bookings) {
        delegate.processFinish(bookings);
    }
}
