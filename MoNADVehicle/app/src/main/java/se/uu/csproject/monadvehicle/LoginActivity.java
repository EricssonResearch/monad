package se.uu.csproject.monadvehicle;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.mapsforge.map.android.graphics.AndroidGraphicFactory;

public class LoginActivity extends AppCompatActivity {

    EditText usernameField;
    EditText passwordField;
    EditText busNumberField;
    Button loginButton;
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
                if(usernameField.getText().length() >= 0
                        && passwordField.getText().length() >= 0
                        && busNumberField.getText().length() >= 0) {
                    startActivity(new Intent(v.getContext(), MainActivity.class));
                }
            }
        });

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
}
