package se.uu.csproject.monadclient.serverinteractions;

import android.os.AsyncTask;

import se.uu.csproject.monadclient.interfaces.AsyncResponseString;

public class SendUpdateFeedbackRequest extends AsyncTask<String, Void, String> {
    public AsyncResponseString delegate = null;

    /* This is the function that is called by the button listener */
    @Override
    protected String doInBackground(String... params) {
        String request = "/updateFeedbackRequest";
        String urlParameters = "changedFeedback=" + params[0];
        return ConnectToRequestHandler.postRequestString(request, urlParameters);
    }

    /* Deal with the response returned by the server */
    @Override
    protected void onPostExecute(String response) {
        delegate.processFinish(response);
    }
}
