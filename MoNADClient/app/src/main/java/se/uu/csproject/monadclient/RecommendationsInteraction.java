package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

import se.uu.csproject.monadclient.recyclerviews.Storage;

/**
 *
 */
public class RecommendationsInteraction {
    String callingClassName;

    private class GetRecommendationsTask extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            String response = ClientAuthentication.postGetRecommendationsRequest();
            Log.i("Recommendations: ", response);
            return response;
        }
    }

    public RecommendationsInteraction(String callingClassName) {
        this.callingClassName = callingClassName;
    }

    public void getRecommendations() {
//        Storage.initializeRecommendationsData();
        GetRecommendationsTask recommendationsTask = new GetRecommendationsTask();

        try {
            String response = recommendationsTask.execute().get();
            System.out.println("Response: " + response);

            if (response.equals("1")) {
                Log.d(this.callingClassName, "Recommendations have been successfully loaded by the database");
            }
            else {
                //initialize notifications, temporary
                Storage.initializeRecommendationsData();
                Log.d(this.callingClassName, "Fake recommendations have been generated");
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            Storage.initializeRecommendationsData();
            Log.d(this.callingClassName,
                    "Exception while loading recommendations - Fake recommendations have been generated");
        }
    }

}
