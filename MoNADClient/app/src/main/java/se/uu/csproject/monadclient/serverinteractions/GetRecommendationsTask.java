package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.interfaces.AsyncRecommendationsInteraction;

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
            Log.d(callingClass.getClass().getCanonicalName(),
                    "Recommendations have been successfully loaded by the database");
        }
        else {
            Log.d(callingClass.getClass().getCanonicalName(),
                    "Could not load recommendations");
        }
        callingClass.processReceivedRecommendations();
    }
}