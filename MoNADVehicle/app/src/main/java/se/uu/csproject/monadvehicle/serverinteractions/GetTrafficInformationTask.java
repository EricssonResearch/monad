package se.uu.csproject.monadvehicle.serverinteractions;

import android.os.AsyncTask;

import se.uu.csproject.monadvehicle.interfaces.AsyncGetTrafficInformationInteraction;

/**
 *
 */
public class GetTrafficInformationTask extends AsyncTask<Void, Void, String> {
    AsyncGetTrafficInformationInteraction callingClass;

    public GetTrafficInformationTask(AsyncGetTrafficInformationInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        return VehicleAdministration.postGetTrafficInformationRequest();
    }

    @Override
    protected void onPostExecute(String response) {
        callingClass.processReceivedGetTrafficInformationResponse(response);
    }
}
