package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;

public class SendResetPasswordRequest extends AsyncTask<String, Void, String> {

    /* This is the function that is called by the button listener */
    @Override
    protected String doInBackground(String... params) {
        String request = "/resetPassword";
        String urlParameters = "email=" + params[0];
        return ConnectToRequestHandler.postRequestString(request, urlParameters);
    }

    /* Deal with the response returned by the server */
    @Override
    protected void onPostExecute(String response) {

    }
}
