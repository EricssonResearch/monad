package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

/* put the LogInRequest in the background and post it */
public class LoginTask extends AsyncTask <String, Void, String> {
    private AsyncLoginInteraction callingClass;

    public LoginTask(AsyncLoginInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected String doInBackground(String... params) {
        return ClientAuthentication.postSignInRequest(params[0], params[1]);
    }

    @Override
    protected void onPostExecute(String response) {
        callingClass.processReceivedLoginResponse(response);
    }
}