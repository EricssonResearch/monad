package se.uu.csproject.monadvehicle;

import android.os.AsyncTask;

/**
 *
 */
public class GetNextTripTask extends AsyncTask<Void, Void, String> {
    private AsyncGetNextTripInteraction callingClass;

    public GetNextTripTask(AsyncGetNextTripInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        return VehicleAdministration.postGetNextTripRequest();
    }

    @Override
    protected void onPostExecute(String response) {
        callingClass.processReceivedLoginResponse(response);
    }

}
