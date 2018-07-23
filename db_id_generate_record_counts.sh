for F in projectcode nucleicacidtype sampletype sequencingtype jaxiddetail; do
    myr jaxid_db_prod <<<"select count(*) as count_${F} from id_generate_${F};";
done
