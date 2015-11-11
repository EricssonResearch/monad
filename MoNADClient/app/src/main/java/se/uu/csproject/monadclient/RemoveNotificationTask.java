package se.uu.csproject.monadclient;

import android.os.AsyncTask;

/**
 *
 */
public class RemoveNotificationTask extends AsyncTask<String, Void, String> {

    @Override
    protected String doInBackground(String... params) {
        String response = ClientAuthentication.postRemoveNotificationRequest(params[0]);
//        Log.i("Notifications: ", response);
        return response;
    }
}