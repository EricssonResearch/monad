package se.uu.csproject.monadvehicle.serverinteractions;

import android.os.AsyncTask;

import se.uu.csproject.monadvehicle.interfaces.AsyncSetGoogleRegistrationTokenInteraction;

/**
 *
 */
public class SetGoogleRegistrationTokenTask extends AsyncTask<Void, Void, String> {
    private AsyncSetGoogleRegistrationTokenInteraction callingClass;

    public SetGoogleRegistrationTokenTask(AsyncSetGoogleRegistrationTokenInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        return VehicleAdministration.postSetGoogleRegistrationTokenRequest();
    }

    @Override
    protected void onPostExecute(String response) {
        callingClass.processSetGoogleRegistrationTokenResponse(response);
    }

}
