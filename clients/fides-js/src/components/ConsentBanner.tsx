import { h, FunctionComponent } from "preact";
import { useState, useEffect } from "preact/hooks";
import { ButtonType, ExperienceConfig } from "../lib/consent-types";
import Button from "./Button";
import { useHasMounted } from "../lib/hooks";

interface BannerProps {
  experience: ExperienceConfig;
  onAcceptAll: () => void;
  onRejectAll: () => void;
  waitBeforeShow?: number;
  managePreferencesLabel?: string;
  onOpenModal: () => void;
}

const ConsentBanner: FunctionComponent<BannerProps> = ({
  experience,
  onAcceptAll,
  onRejectAll,
  waitBeforeShow,
  onOpenModal,
}) => {
  const [isShown, setIsShown] = useState(false);
  const hasMounted = useHasMounted();
  const {
    title = "Manage your consent",
    description = "This website processes your data respectfully, so we require your consent to use cookies.",
    accept_button_label: acceptButtonLabel = "Accept All",
    reject_button_label: rejectButtonLabel = "Reject All",
    privacy_preferences_link_label:
      privacyPreferencesLabel = "Manage preferences",
  } = experience;

  useEffect(() => {
    const delayBanner = setTimeout(() => {
      setIsShown(true);
    }, waitBeforeShow);
    return () => clearTimeout(delayBanner);
  }, [setIsShown, waitBeforeShow]);

  const handleManagePreferencesClick = (): void => {
    onOpenModal();
    setIsShown(false);
  };

  if (!hasMounted) {
    return null;
  }

  return (
    <div
      id="fides-banner"
      className={`fides-banner fides-banner-bottom ${
        isShown ? "" : "fides-banner-hidden"
      } `}
    >
      <div id="fides-banner-inner">
        <div id="fides-banner-title" className="fides-banner-title">
          {title}
        </div>
        <div id="fides-banner-description" className="fides-banner-description">
          {description}
        </div>
        <div id="fides-banner-buttons" className="fides-banner-buttons">
          <span className="fides-banner-buttons-left">
            <Button
              buttonType={ButtonType.TERTIARY}
              label={privacyPreferencesLabel}
              onClick={handleManagePreferencesClick}
            />
          </span>
          <span className="fides-banner-buttons-right">
            <Button
              buttonType={ButtonType.PRIMARY}
              label={rejectButtonLabel}
              onClick={() => {
                onRejectAll();
                setIsShown(false);
              }}
            />
            <Button
              buttonType={ButtonType.PRIMARY}
              label={acceptButtonLabel}
              onClick={() => {
                onAcceptAll();
                setIsShown(false);
              }}
            />
          </span>
        </div>
      </div>
    </div>
  );
};

export default ConsentBanner;
