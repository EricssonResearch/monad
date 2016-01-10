package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;

import se.uu.csproject.monadclient.interfaces.AsyncLoginInteraction;
import se.uu.csproject.monadclient.serverinteractions.ClientAuthentication;

/* put the LogInRequest in the background and post it */
public class LoginTask extends AsyncTask <String, Void, String> {
    private AsyncLoginInteraction callingClass;

    public LoginTask(AsyncLoginInteraction callingClass) {
        this.callingClass = callingClass;
    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();
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