package se.uu.csproject.monadvehicle;

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

import org.mapsforge.map.android.graphics.AndroidGraphicFactory;

public class LoginActivity extends AppCompatActivity implements AsyncLoginInteraction, AsyncGetNextTripInteraction {
    private EditText usernameField;
    private EditText passwordField;
    private EditText busNumberField;
    private Button loginButton;
    //ToggleButton emergencyButton;

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

        //// TODO: add login authentication for vehicle app, similar to that in client app
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                login();
//                if(usernameField.getText().length() >= 0
//                        && passwordField.getText().length() >= 0
//                        && busNumberField.getText().length() >= 0) {
//                    startActivity(new Intent(v.getContext(), MainActivity.class));
//                }
            }
        });

        // Hides the keyboard on display
        this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);

        /*emergencyButton.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    // The toggle is enabled
                } else {
                    // The toggle is disabled
                }
            }
        });*/
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_login, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        return super.onOptionsItemSelected(item);
    }

    public void login() {
        new LoginTask(this).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR,
                usernameField.getText().toString(),
                passwordField.getText().toString(),
                busNumberField.getText().toString());
    }

    @Override
    public void processReceivedLoginResponse(String response) {

        /* If the response starts with the specific word, it means the user logged in successfully */
        if (response.startsWith("Success (1)")) {
            Log.d("LoginActivity", "Successfully signed in");
            getNextTrip();
        }
        else if (response.equals("Wrong Credentials (0)")) {
            Log.d("LoginActivity", "Wrong credentials");
            Toast.makeText(getApplicationContext(), "Wrong credentials", Toast.LENGTH_LONG).show();
        }
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

        if (response.equals("1")) {
            Log.d("LoginActivity", "Successfully received BusTrip data");

            try {
                LoginActivity.this.startActivity(new Intent(LoginActivity.this, MainActivity.class));
            }
            catch (Exception e) {
                e.printStackTrace();
            }
            finally {
                finish();
            }
        }
        else {
            Log.d("LoginActivity", "Error while receiving BusTrip data");
            LoginActivity.this.startActivity(new Intent(LoginActivity.this, LoginActivity.class));
            finish();
        }
    }
}