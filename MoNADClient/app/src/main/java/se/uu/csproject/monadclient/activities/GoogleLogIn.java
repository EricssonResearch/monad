package se.uu.csproject.monadclient.activities;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.IntentSender;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.common.Scopes;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.GoogleApiClient.OnConnectionFailedListener;
import com.google.android.gms.common.api.Scope;
import com.google.android.gms.plus.Plus;

import java.util.concurrent.ExecutionException;

import se.uu.csproject.monadclient.serverinteractions.ClientAuthentication;
import se.uu.csproject.monadclient.R;

public class GoogleLogIn extends Activity implements
        GoogleApiClient.ConnectionCallbacks,
        OnConnectionFailedListener,
        OnClickListener {

    private Context context;
    private final int MY_PERMISSIONS_REQUEST = 123;
    private static final int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
    private static final int SIGN_IN_REQUEST_CODE = 10;
    /* Is there a ConnectionResult resolution in progress? */
    private boolean mIsResolving = false;

    /* Should we automatically resolve ConnectionResults when possible? */
    private boolean mShouldResolve = false;

    /* Request code used to invoke sign in user interactions. */
    private static final int RC_SIGN_IN = 0;

    /* Client used to interact with Google APIs. */
    private GoogleApiClient mGoogleApiClient;
    private boolean mIntentInProgress;

    //  a tag when printing log messages to the console (ddms)
    public static final String TAG = "MoNAD";

    // contains all possible error codes for when a client fails to connect to
    // Google Play services
    private ConnectionResult mConnectionResult;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        context = getApplicationContext();

        // Build GoogleApiClient with access to basic profile
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(Plus.API)
                .addScope(new Scope(Scopes.PROFILE))
                .addScope(new Scope(Scopes.EMAIL))
                .build();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (checkPlayServices()){
            if (!mGoogleApiClient.isConnected()) {
                if (Build.VERSION.SDK_INT >= 23){
                    checkForPermission();
                } else {
                    mGoogleApiClient.connect();
                }
            }
        } else {
            CharSequence text = getString(R.string.java_googleplayloginwarning);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_LONG);
            toast.show();
        }
    }

    @Override
    protected void onStop() {
        super.onStop();
        // disconnect api if it is connected
        if (mGoogleApiClient.isConnected())
            mGoogleApiClient.disconnect();
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.google_login_button) {
            onSignInClicked();
        }
    }

    private void onSignInClicked() {
        // User clicked the sign-in button, so begin the sign-in process and automatically
        // attempt to resolve any errors that occur.
        mShouldResolve = true;
        mGoogleApiClient.connect();
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Log.d(TAG, "onActivityResult:" + requestCode + ":" + resultCode + ":" + data);

        if (requestCode == RC_SIGN_IN) {
            // If the error resolution was not successful we should not resolve further.
            if (resultCode != RESULT_OK) {
                mShouldResolve = false;
            }

            mIsResolving = false;
            mGoogleApiClient.connect();
        }
    }

    @Override
    public void onConnected(Bundle bundle) {
        // onConnected indicates that an account was selected on the device, that the selected
        // account has granted any requested permissions to our app and that we were able to
        // establish a service connection to Google Play services.

        String email = Plus.AccountApi.getAccountName(mGoogleApiClient);

        GoogleSignUpTask googleSignUpTask = new GoogleSignUpTask();
        try {
            String response = googleSignUpTask.execute(email).get();
            //Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();

            if (response.startsWith("Success (1)")) {
                GoogleLogIn.this.startActivity(new Intent(GoogleLogIn.this, MainActivity.class));
                setResult(RESULT_OK);
                finish();
            }
            else {
                GoogleLogIn.this.startActivity(new Intent(GoogleLogIn.this, LoginActivity.class));
                finish();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
            GoogleLogIn.this.startActivity(new Intent(GoogleLogIn.this, LoginActivity.class));
            finish();
        } catch (ExecutionException e) {
            e.printStackTrace();
            GoogleLogIn.this.startActivity(new Intent(GoogleLogIn.this, LoginActivity.class));
            finish();
        }
    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    public void onConnectionFailed(ConnectionResult result) {
        if (!mIntentInProgress && result.hasResolution()) {
            try {
                mIntentInProgress = true;
                startIntentSenderForResult(result.getResolution().getIntentSender(),
                        RC_SIGN_IN, null, 0, 0, 0);
            } catch (IntentSender.SendIntentException e) {
                // The intent was canceled before it was sent.  Return to the default
                // state and attempt to connect to get an updated ConnectionResult.
                mIntentInProgress = false;
                mGoogleApiClient.connect();
            }
        }
    }

    private class GoogleSignUpTask extends AsyncTask<String, Void, String>{

        @Override
        protected String doInBackground(String... params) {
            String response = ClientAuthentication.postGoogleSignInRequest(params[0]);
            return response;
        }
    }

    // Checks if the user has given google account permission and asks for it if he hasn't
    private void checkForPermission(){
        if (ContextCompat.checkSelfPermission(GoogleLogIn.this, Manifest.permission.GET_ACCOUNTS)
                != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(GoogleLogIn.this,
                    new String[]{Manifest.permission.GET_ACCOUNTS}, MY_PERMISSIONS_REQUEST);
        } else {
            mGoogleApiClient.connect();
        }
    }

    // Checks the result of the permission asked of the user
    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    mGoogleApiClient.connect();
                } else {
                    // Permission denied, boo! Disable the functionality that depends on this permission.
                    CharSequence text = getString(R.string.java_accountpermissionwarning);
                    Toast toast = Toast.makeText(context, text, Toast.LENGTH_LONG);
                    toast.show();
                }
                break;
            }
        }
    }

    // Checks if the user has google play services enabled
    private boolean checkPlayServices() {
        GoogleApiAvailability apiAvailability = GoogleApiAvailability.getInstance();
        int resultCode = apiAvailability.isGooglePlayServicesAvailable(this);
        if (resultCode != ConnectionResult.SUCCESS) {
            if (apiAvailability.isUserResolvableError(resultCode)) {
                apiAvailability.getErrorDialog(this, resultCode, PLAY_SERVICES_RESOLUTION_REQUEST).show();
            }
            return false;
        }
        return true;
    }
}