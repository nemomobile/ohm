/**
 * @file hal.c
 * @brief OHM HAL plugin 
 * @author ismo.h.puustinen@nokia.com
 *
 * Copyright (C) 2008, Nokia. All rights reserved.
 */

#include "hal.h"

hal_plugin *hal_plugin_p = NULL;

static void
plugin_init(OhmPlugin * plugin)
{
    DBusConnection *c = ohm_plugin_dbus_get_connection();
    g_print("> HAL plugin init\n");
    /* should we ref the connection? */
    hal_plugin_p = init_hal(c);
    g_print("< HAL plugin init\n");
    return;
}

/**
 * Marks the udi as interesting. Interesting HAL devices are mapped to
 * factstore.
 */
OHM_EXPORTABLE(gboolean, interested, (gchar *udi))
{
    return mark_interesting(hal_plugin_p, udi);
}

/**
 * Marks the udi as uninteresting.
 */
OHM_EXPORTABLE(gboolean, uninterested, (gchar *udi))
{
    return mark_uninteresting(hal_plugin_p, udi);
}

static void
plugin_exit(OhmPlugin * plugin)
{
    if (hal_plugin_p) {
        deinit_hal(hal_plugin_p);
    }
    g_free(hal_plugin_p);
    return;
}

OHM_PLUGIN_DESCRIPTION("hal",
        "0.0.1",
        "ismo.h.puustinen@nokia.com",
        OHM_LICENSE_NON_FREE, plugin_init, plugin_exit,
        NULL);

OHM_PLUGIN_PROVIDES_METHODS(hal, 2,
        OHM_EXPORT(interested, "interested"),
        OHM_EXPORT(uninterested, "uninterested"));
/*
 * Local Variables:
 * c-basic-offset: 4
 * indent-tabs-mode: nil
 * End:
 * vim:set expandtab shiftwidth=4:
 */
