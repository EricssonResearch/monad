package se.uu.csproject.monadvehicle.activities;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;

import org.mapsforge.map.android.graphics.AndroidGraphicFactory;

import se.uu.csproject.monadvehicle.serverinteractions.LoginTask;
import se.uu.csproject.monadvehicle.R;
import se.uu.csproject.monadvehicle.googlecloudmessaging.RegistrationIntentService;
import se.uu.csproject.monadvehicle.interfaces.AsyncGetNextTripInteraction;
import se.uu.csproject.monadvehicle.interfaces.AsyncGetTrajectoryInteraction;
import se.uu.csproject.monadvehicle.interfaces.AsyncLoginInteraction;
import se.uu.csproject.monadvehicle.serverinteractions.GetNextTripTask;
import se.uu.csproject.monadvehicle.serverinteractions.GetTrajectoryTask;

public class LoginActivity extends AppCompatActivity implements AsyncLoginInteraction, AsyncGetNextTripInteraction,
        AsyncGetTrajectoryInteraction {
    private EditText usernameField;
    private EditText passwordField;
    private EditText busNumberField;
    private Button loginButton;
    //ToggleButton emergencyButton;

    /* Google Cloud Services */
    private static final String TAG = "MainActivity";
    private static final int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        AndroidGraphicFactory.createInstance(this.getApplication());
        setContentView(R.layout.activity_login);

        usernameField = (EditText) findViewById(R.id.usernameField);
        passwordField = (EditText) findViewById(R.id.passwordField);
        busNumberField = (EditText) findViewById(R.id.busNumberField);
        loginButton = (Button) findViewById(R.id.loginButton);
        //emergencyButton = (ToggleButton) findViewById(R.id.emergencyButton);

        if (checkPlayServices()) {
            Intent intent = new Intent(this,RegistrationIntentService.class);
            startService(intent);
        }

        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                login();
            }
        });

        /* Hides the keyboard on display */
        this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);

        /*
        emergencyButton.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    // The toggle is enabled
                } else {
                    // The toggle is disabled
                }
            }
        });
        */
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        /* Inflate the menu; this adds items to the action bar if it is present. */
        getMenuInflater().inflate(R.menu.menu_login, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        /*
         * Handle action bar item clicks here. The action bar will
         * automatically handle clicks on the Home/Up button, so long
         * as you specify a parent activity in AndroidManifest.xml.
         */
        int id = item.getItemId();
        return super.onOptionsItemSelected(item);
    }

    public void login() {
        new LoginTask(this).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, usernameField.getText().toString(),
                                              passwordField.getText().toString(), busNumberField.getText().toString());
    }

    @Override
    public void processReceivedLoginResponse(String response) {

        /* If the response starts with the specific string, it means the user logged in successfully */
        if (response.startsWith("Success (1)")) {
            Log.d("LoginActivity", "Successfully signed in");
            getNextTrip();
        }
        /* Wrong credentials have been provided */
        else if (response.equals("Wrong Credentials (0)")) {
            Log.d("LoginActivity", "Wrong credentials");
            Toast.makeText(getApplicationContext(), "Wrong credentials", Toast.LENGTH_LONG).show();
        }
        /* An exception occurred while interacting with the Route Administrator */
        else {
            Log.d("LoginActivity", "ERROR - login");
            Toast.makeText(getApplicationContext(), "ERROR - login", Toast.LENGTH_LONG).show();
            LoginActivity.this.startActivity(new Intent(LoginActivity.this, LoginActivity.class));
            finish();
        }
    }

    public void getNextTrip() {
        new GetNextTripTask(this).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
    }

    @Override
    public void processReceivedGetNextTripResponse(String response) {

        /* Successful interaction between the application and the Route Administrator */
        if (response.equals("1")) {
            Log.d("LoginActivity", "Successfully received BusTrip data");
            getTrajectory();
        }
        /* An exception occurred while interacting with the Route Administrator */
        else {
            Log.d("LoginActivity", "Error while receiving BusTrip data");
            LoginActivity.this.startActivity(new Intent(LoginActivity.this, LoginActivity.class));
            finish();
        }
    }

    public void getTrajectory() {
        new GetTrajectoryTask(this).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
    }

    @Override
    public void processGetTrajectoryResponse(String response) {
        try {
            Log.d("LoginActivity", "Received trajectory response");
            LoginActivity.this.startActivity(new Intent(LoginActivity.this, MainActivity.class));
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            finish();
        }
    }

    private boolean checkPlayServices() {
        GoogleApiAvailability apiAvailability = GoogleApiAvailability.getInstance();
        int resultCode = apiAvailability.isGooglePlayServicesAvailable(this);
        if (resultCode != ConnectionResult.SUCCESS) {
            if (apiAvailability.isUserResolvableError(resultCode)) {
                apiAvailability.getErrorDialog(this, resultCode, PLAY_SERVICES_RESOLUTION_REQUEST)
                        .show();
            } else {
                Log.i(TAG, "This device is not supported.");
                finish();
            }
            return false;
        }
        return true;
    }

}

