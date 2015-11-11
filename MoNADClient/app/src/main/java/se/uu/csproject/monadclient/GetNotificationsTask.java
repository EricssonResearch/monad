package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

/**
 *
 */
public class GetNotificationsTask extends AsyncTask<String, Void, String> {

    @Override
    protected String doInBackground(String... params) {
        String response = ClientAuthentication.postGetNotificationsRequest();
//        Log.i("Notifications: ", response);
        return response;
    }
}