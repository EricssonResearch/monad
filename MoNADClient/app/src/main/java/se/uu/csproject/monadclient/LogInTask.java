package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

/* put the LogInRequest in the background and post it */
public class LogInTask extends AsyncTask <String, Void, String> {

    @Override
    protected String doInBackground(String... params) {
        String response = ClientAuthentication.postSignInRequest(params[0], params[1]);

        Log.i("SignUpResponse", response);

        return response;
    }
}