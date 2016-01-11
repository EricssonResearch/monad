package se.uu.csproject.monadvehicle.serverinteractions;

import android.os.AsyncTask;

import se.uu.csproject.monadvehicle.interfaces.AsyncGetTrajectoryInteraction;

/**
 *
 */
public class GetTrajectoryTask extends AsyncTask<Void, Void, String> {
    private AsyncGetTrajectoryInteraction callingClass;

    public GetTrajectoryTask(AsyncGetTrajectoryInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        return VehicleAdministration.postGetTrajectoryRequest();
    }

    @Override
    protected void onPostExecute(String response) {
        callingClass.processGetTrajectoryResponse(response);
    }
}
