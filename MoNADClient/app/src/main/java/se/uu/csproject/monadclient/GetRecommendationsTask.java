package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.ClientAuthentication;

/**
 *
 */
public class GetRecommendationsTask extends AsyncTask<String, Void, String> {

    @Override
    protected String doInBackground(String... params) {
        String response = ClientAuthentication.postGetRecommendationsRequest();
        Log.i("Recommendations: ", response);
        return response;
    }
}