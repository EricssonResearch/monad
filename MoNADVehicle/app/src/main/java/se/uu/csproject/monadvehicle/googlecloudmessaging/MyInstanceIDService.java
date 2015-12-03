package se.uu.csproject.monadvehicle.googlecloudmessaging;


import android.app.IntentService;
import android.content.Intent;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.util.Log;

import com.google.android.gms.gcm.GoogleCloudMessaging;
import com.google.android.gms.iid.InstanceID;
import com.google.android.gms.iid.InstanceIDListenerService;

import se.uu.csproject.monadvehicle.R;
import java.io.IOException;



public class MyInstanceIDService extends IntentService {

    private static final String TAG = "RegistrationIntentSrv";


    public MyInstanceIDService() {
        super("MyInstanceIDService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        InstanceID instanceID = InstanceID.getInstance(this);
        //R.string.gcm_defaultSenderId (the Sender ID) is typically derived from google-services.json.
        try {
            String token = instanceID.getToken(getString(R.string.gcm_defaultSenderId),
                    GoogleCloudMessaging.INSTANCE_ID_SCOPE, null);
        } catch (Exception e) {
            Log.d(TAG, "Failed in token refresh", e);
        }
    }
}