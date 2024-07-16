from phonepe import PhonePe


def create_phonepe_instance(merchant_id, phone_pe_salt, phone_pe_host, redirect_url, webhook_url):
    return PhonePe(
        merchant_id=merchant_id,
        phone_pe_salt=phone_pe_salt,
        phone_pe_host=phone_pe_host,
        redirect_url=redirect_url,
        webhook_url=webhook_url
    )