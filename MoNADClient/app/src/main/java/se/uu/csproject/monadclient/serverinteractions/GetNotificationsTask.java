package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.interfaces.AsyncNotificationsInteraction;

public class GetNotificationsTask extends AsyncTask<Void, Void, String> {
    private AsyncNotificationsInteraction callingClass;

    public GetNotificationsTask(AsyncNotificationsInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        return ClientAuthentication.postGetNotificationsRequest();
    }

    @Override
    protected void onPostExecute(String response) {

        if (response.equals("1")) {
            Log.d(callingClass.getClass().getCanonicalName(),
                    "Notifications have been successfully loaded by the database");
        }
        else {
            Log.d(callingClass.getClass().getCanonicalName(), "Could not load notifications");
        }
        callingClass.processReceivedNotifications();
    }
}
