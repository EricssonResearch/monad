package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

/* put the SignUpRequest in the background and post it */
public class SignUpTask extends AsyncTask <String, Void, String> {

    @Override
    protected String doInBackground(String... params) {
        String response = ClientAuthentication.postSignUpRequest(params[0], params[1], params[2], params[3]);

        Log.i("SignUpResponse", response);

        return response;
    }

}
