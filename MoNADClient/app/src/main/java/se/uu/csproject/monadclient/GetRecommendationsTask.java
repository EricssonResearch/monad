package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.interfaces.AsyncRecommendationsInteraction;
import se.uu.csproject.monadclient.storage.Storage;

/**
 *
 */
public class GetRecommendationsTask extends AsyncTask<Void, Void, String> {
    AsyncRecommendationsInteraction callingClass;

    public GetRecommendationsTask(AsyncRecommendationsInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(Void... params) {
        String response = ClientAuthentication.postGetRecommendationsRequest();
        return response;
    }

    @Override
    protected void onPostExecute(String response) {
        if (response.equals("1")) {
            Log.d(callingClass.getClass().getCanonicalName(), "Recommendations have been successfully loaded by the database");
        }
        else {
            //initialize notifications, temporary
            Storage.initializeRecommendationsData();
            Log.d(callingClass.getClass().getCanonicalName(), "Fake recommendations have been generated");
        }
        callingClass.processReceivedRecommendations();
    }
}