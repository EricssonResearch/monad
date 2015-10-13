package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputType;
import android.util.DisplayMetrics;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;


public class ProfileEditPopup extends AppCompatActivity {
    private Button button_editprofile_cancel;
    private TextView textview_editprofile_name;
    private EditText edittext_editprofile_textfield;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_profile_edit);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width * .9), (int) (height * .33));

        Intent intent = getIntent();
        String name = intent.getStringExtra("name");
        changeProfileText(name);

        button_editprofile_cancel = (Button)findViewById(R.id.button_editprofile_btncancel);
        button_editprofile_cancel.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                startActivity(new Intent(ProfileEditPopup.this, ProfileActivity.class));
            }
        });

    }

    public void changeProfileText(String name){
        //handles textview and textfield changes and
        // set values on changing profile text
        textview_editprofile_name = (TextView)findViewById(R.id.textview_editprofile_textfieldname);
        edittext_editprofile_textfield = (EditText)findViewById(R.id.edittext_editprofile_editfield);
        if(name.equals("username")){
            textview_editprofile_name.setText("Username :");
            edittext_editprofile_textfield.setInputType(InputType.TYPE_CLASS_TEXT);
        }
        if(name.equals("phone")){
            textview_editprofile_name.setText("Phone No. :");
            edittext_editprofile_textfield.setInputType(InputType.TYPE_CLASS_PHONE);
        }
        if(name.equals("email")){
            textview_editprofile_name.setText("Email :");
            edittext_editprofile_textfield.setInputType(InputType.TYPE_TEXT_VARIATION_WEB_EMAIL_ADDRESS);
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
