import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config('RK SIR STUDENTS')


# Load the DataFrame
excel_file = 'C:\\Users\\ANIL\\Documents\\Projects\\RK\\rk_data.xlsx'
sheet_name = 'DATA'
df = pd.read_excel(excel_file, sheet_name=sheet_name)

st.header('STUDENTS DATA')


# Choose an Action
action = st.selectbox(
    "Choose an Action",
    [
        "DATA VIEWING",
        "DATA ENTRY",
        "UPDATE EXISTING ENTRY",
        "DELETE ENTRY",
        
    ],
)

# Based on the selected action, display the relevant information
if action == "DATA VIEWING":
    # Display the original data again
    st.header('DATA VIEWING')
    st.dataframe(df)

elif action == "DATA ENTRY":
    # Display the original data
    st.header('ORIGINAL DATA')
    st.dataframe(df)
    # Display the data entry form
    st.header('DATA ENTRY')
    st.markdown("Enter the details of the new student below.")
    
    # Take input for new data
    st.subheader('Enter New Data')

    # Use st.form() to wrap the form elements
    with st.form(key='my_form'):
        student_name = st.text_input('Student Name*')
        grade = st.text_input('Grade*')
        date_of_joining = st.date_input('Date of Joining*')
        subject = st.text_input('Subject*')
        fees = st.number_input('Fees*')
        amount_paid = st.number_input('Amount Paid*')

        # Mark mandatory fields
        st.markdown("**required*")

        # st.form_submit_button should be used inside the st.form() context
        submit_button = st.form_submit_button(label="Submit Vendor Details")

    if submit_button:
        # Update the DataFrame with new data
        new_data = {'Student Name': [student_name],
                    'Grade': [grade],
                    'Date of Joining': [pd.to_datetime(date_of_joining)],  # Convert to datetime
                    'Subject': [subject],
                    'Fees': [fees],
                    'Amount Paid': [amount_paid]}

        new_df = pd.DataFrame(new_data)
        df = pd.concat([df, new_df], ignore_index=True)

        # Display the updated DataFrame
        st.subheader('Updated Data')
        st.success("Vendor details successfully submitted!")
        # Convert 'Date of Joining' to string before displaying
        df_display = df.copy()
        df_display['Date of Joining'] = df_display['Date of Joining'].dt.strftime('%Y-%m-%d')

        st.dataframe(df_display)

elif action == "UPDATE EXISTING ENTRY":
    # Display the original data
    st.header('ORIGINAL DATA')
    st.dataframe(df)
    
    # Display the update form
    st.header('UPDATE EXISTING ENTRY')
    st.markdown("Enter the details to update the existing student entry.")
    
    # Take input for existing data to be updated
    st.subheader('Enter Existing Data for Update')

    # Use st.form() to wrap the form elements
    with st.form(key='update_form'):
        # Dropdown to select existing student for update
        student_to_update = st.selectbox('Select Student to Update', df['Student Name'])
        # Input fields for update
        updated_grade = st.text_input('Updated Grade')
        updated_date_of_joining = st.date_input('Updated Date of Joining')
        updated_subject = st.text_input('Updated Subject')
        updated_fees = st.number_input('Updated Fees')
        updated_amount_paid = st.number_input('Updated Amount Paid')

        # st.form_submit_button should be used inside the st.form() context
        update_button = st.form_submit_button(label="Update Vendor Details")

    if update_button:
        # Update the DataFrame with the edited data
        df.loc[df['Student Name'] == student_to_update, 'Grade'] = updated_grade
        df.loc[df['Student Name'] == student_to_update, 'Date of Joining'] = pd.to_datetime(updated_date_of_joining)
        df.loc[df['Student Name'] == student_to_update, 'Subject'] = updated_subject
        df.loc[df['Student Name'] == student_to_update, 'Fees'] = updated_fees
        df.loc[df['Student Name'] == student_to_update, 'Amount Paid'] = updated_amount_paid

        # Display the updated DataFrame
        st.subheader('Updated Data')
        st.success("Vendor details successfully updated!")
        # Convert 'Date of Joining' to string before displaying
        df_display = df.copy()
        df_display['Date of Joining'] = df_display['Date of Joining'].dt.strftime('%Y-%m-%d')

        st.dataframe(df_display)

elif action == "DELETE ENTRY":
    # Display the original data
    st.header('ORIGINAL DATA')
    st.dataframe(df)
    
    # Display the delete form
    st.header('DELETE ENTRY')
    st.markdown("Enter the details to delete the existing student entry.")
    
    # Take input for existing data to be deleted
    st.subheader('Enter Existing Data for Deletion')

    # Use st.form() to wrap the form elements
    with st.form(key='delete_form'):
        # Dropdown to select existing student for deletion
        student_to_delete = st.selectbox('Select Student to Delete', df['Student Name'])

        # st.form_submit_button should be used inside the st.form() context
        delete_button = st.form_submit_button(label="Delete Vendor Details")

    if delete_button:
        # Delete the selected row from the DataFrame
        df = df[df['Student Name'] != student_to_delete]

        # Save the modified DataFrame back to the Excel file
        df.to_excel(excel_file, sheet_name=sheet_name, index=False)

        # Display the updated DataFrame
        st.subheader('Updated Data')
        st.success("Vendor details successfully deleted!")
        # Convert 'Date of Joining' to string before displaying
        df_display = df.copy()
        df_display['Date of Joining'] = df_display['Date of Joining'].dt.strftime('%Y-%m-%d')
        st.dataframe(df_display)
