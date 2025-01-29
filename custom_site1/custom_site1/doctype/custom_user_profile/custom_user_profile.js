// Copyright (c) 2025, me and contributors
// For license information, please see license.txt

frappe.ui.form.on("Custom User Profile", {
  refresh(frm) {
    frm.fields_dict.category.get_query = function (doc) {
      return {
        filters: {
          data: "two",
        },
      };
    };
  },
});
