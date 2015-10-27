package se.uu.csproject.monadclient;

import android.os.AsyncTask;
import android.util.Log;

public class UpdateProfileTask extends AsyncTask<String, Void, String>{
    @Override
    protected String doInBackground(String... params) {
        String response = ClientAuthentication.postProfileUpdateRequest(params[0], params[1], params[2], params[3]);

        Log.i("UpdateProfileResponse", response);

        return response;
    }
}
