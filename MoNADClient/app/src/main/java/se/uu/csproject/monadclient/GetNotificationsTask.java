package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.interfaces.AsyncNotificationsInteraction;
import se.uu.csproject.monadclient.recyclerviews.Storage;

/**
 *
 */
public class GetNotificationsTask extends AsyncTask<Void, Void, String> {
    private AsyncNotificationsInteraction callingClass;

    public GetNotificationsTask(AsyncNotificationsInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        String response = ClientAuthentication.postGetNotificationsRequest();
        return response;
    }

    @Override
    protected void onPostExecute(String response) {

        if (response.equals("1")) {
            Log.d(callingClass.getClass().getCanonicalName(),
                    "Notifications have been successfully loaded by the database");
        }
        else {
            //initialize notifications, temporary
            Storage.initializeNotificationData();
            Log.d(callingClass.getClass().getCanonicalName(), "Fake notifications have been generated");
        }
        callingClass.processReceivedNotifications();
    }
}
