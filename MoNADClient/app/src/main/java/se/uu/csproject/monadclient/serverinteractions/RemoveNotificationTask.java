package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.storage.Storage;

public class RemoveNotificationTask extends AsyncTask<String, Void, String> {
    private int index;

    public RemoveNotificationTask(int index) {
        this.index = index;
    }

    @Override
    protected String doInBackground(String... params) {
        String response = ClientAuthentication.postRemoveNotificationRequest(params[0]);
        return response;
    }

    @Override
    protected void onPostExecute(String response) {

        if (response.equals("1")) {
            Storage.getNotifications().remove(index);
            Log.d("Storage", "Notification was successfully removed from the database");
        }
        else {
            Log.d("Storage", "Notification could not be removed from the database");
        }
    }
}
