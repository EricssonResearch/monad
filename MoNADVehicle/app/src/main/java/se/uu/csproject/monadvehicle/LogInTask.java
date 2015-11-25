package se.uu.csproject.monadvehicle;

import android.os.AsyncTask;
import android.util.Log;

/* put the LogInRequest in the background and post it */
public class LogInTask extends AsyncTask <String, Void, String> {

    @Override
    protected String doInBackground(String... params) {
        String response = VehicleAuthentication.postSignInRequest(params[0], params[1]);

        Log.i("LoginResponse", response);

        return response;
    }
}