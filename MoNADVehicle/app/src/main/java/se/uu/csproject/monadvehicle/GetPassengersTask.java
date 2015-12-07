package se.uu.csproject.monadvehicle;

import android.os.AsyncTask;

/**
 *
 */
public class GetPassengersTask extends AsyncTask<String, Void, String> {
    AsyncGetPassengersInteraction callingClass;

    public GetPassengersTask(AsyncGetPassengersInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(String... params) {
        String response = VehicleAdministration.postGetPassengersRequest(params[0], params[1], params[2]);
        return response;
    }

    @Override
    protected void onPostExecute(String response) {
        callingClass.processReceivedGetPassengersResponse(response);
    }
}
