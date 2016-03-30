from app.event.settings import components, EventWithOneDevice, EventSubSettingsOneDevice


class Add(EventWithOneDevice):
    components = components


class AddSettings(EventSubSettingsOneDevice):
    _schema = Add

