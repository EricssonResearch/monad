package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;
import android.util.Log;

public class RemoveNotificationTask extends AsyncTask<String, Void, String> {

    public RemoveNotificationTask() {}

    @Override
    protected String doInBackground(String... params) {
        String response = ClientAuthentication.postRemoveNotificationRequest(params[0]);
        return response;
    }

    @Override
    protected void onPostExecute(String response) {

        if (response.equals("1")) {
            Log.d("Storage", "Notification was successfully removed from the database");
        }
        else {
            Log.d("Storage", "Notification could not be removed from the database");
        }
    }
}
